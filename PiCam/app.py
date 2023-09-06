import asyncio
from aiortc import RTCPeerConnection, VideoStreamTrack
from config import *
import cv2

async def video_stream():
    cap = cv2.VideoCapture(0)

    while True:
        try:
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame.tostring()
        except :
            print('No Cam')
            pass

async def rtc_handler(reader, writer):
    rtc = RTCPeerConnection()
    video_track = VideoStreamTrack()
    rtc.addTrack(video_track)

    await rtc.setRemoteDescription(await reader.read())
    await rtc.setLocalDescription(await rtc.createAnswer())

    writer.write(b'RTSP/1.0 200 OK\r\n\r\n')
    await writer.drain()
    writer.write(rtc.localDescription.sdp.encode('utf-8'))
    await writer.drain()

    await asyncio.gather(
        video_track.start(video_stream()),
        rtc.negotiate(),
    )

async def main(host, port):
    server = await asyncio.start_server(rtc_handler, host, port)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    host = HOST_IP  # 서버 IP를 설정합니다.
    port = PORT  # RTSP 포트를 설정합니다.
    asyncio.run(main(host, port))
