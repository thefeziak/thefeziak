import asyncio
import sys
import logging
from datetime import datetime

MAIN_PROXY_HOST = "x"
MAIN_PROXY_PORT = 1
LISTEN_PORT = 1

logger = logging.getLogger("forwarder")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

file_handler = logging.FileHandler("forwarder.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def build_proxy_header(real_ip, real_port, local_ip, local_port):
    header = f"PROXY TCP4 {real_ip} {local_ip} {real_port} {local_port}\r\n"
    #logger.debug(f"Built PROXY header: {header.strip()}")
    return header.encode()

async def handle_client(client_reader, client_writer):
    peername = client_writer.get_extra_info("peername")
    if peername is None:
        #logger.warning("Failed to get client peername, closing connection")
        client_writer.close()
        await client_writer.wait_closed()
        return

    real_ip, real_port = peername[0], peername[1]
    #logger.info(f"New connection from {real_ip}:{real_port}")

    try:
        backend_reader, backend_writer = await asyncio.open_connection(MAIN_PROXY_HOST, MAIN_PROXY_PORT)
        local_ip, local_port = backend_writer.get_extra_info("sockname")

        proxy_header = build_proxy_header(real_ip, real_port, local_ip, local_port)
        backend_writer.write(proxy_header)
        await backend_writer.drain()
        #logger.debug(f"Sent PROXY header to backend")

        async def pipe(reader, writer, direction_desc):
            try:
                while True:
                    data = await reader.read(4096)
                    if not data:
                        #logger.debug(f"No data received, ending {direction_desc} pipe")
                        break
                    writer.write(data)
                    await writer.drain()
            except Exception as e:
                pass#logger.warning(f"Error during data transfer ({direction_desc}): {e}")
            finally:
                try:
                    writer.close()
                    await writer.wait_closed()
                    #logger.debug(f"Closed writer ({direction_desc})")
                except Exception:
                    pass

        await asyncio.gather(
            pipe(client_reader, backend_writer, "client->backend"),
            pipe(backend_reader, client_writer, "backend->client")
        )
        #logger.info(f"Connection from {real_ip}:{real_port} closed")

    except Exception as e:
        #logger.error(f"[!] Error connecting to main server: {e}")
        try:
            client_writer.close()
            await client_writer.wait_closed()
        except:
            pass


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', LISTEN_PORT)
    #logger.info(f"Forwarder running on 0.0.0.0:{LISTEN_PORT} → {MAIN_PROXY_HOST}:{MAIN_PROXY_PORT}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass#logger.info("Forwarder manually stopped")

