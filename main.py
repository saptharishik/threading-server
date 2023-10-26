import socket
import cv2
import pickle
import struct
import threading
import time
from n import message  # Assuming n.py contains the message function

def camserver():
    def send_frames(port_no, cam):
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '192.168.1.102'  # Server's IP address
        port = port_no
        socket_address = (host_ip, port)
    
        try:
            server_socket.bind(socket_address)
            server_socket.listen(5)
            print(f"Listening on {socket_address}")
    
            # Accept a connection from the client
            client_socket, addr = server_socket.accept()
            print(f"Connection from: {addr}")
    
            # Open the camera (change 0 to another number if using a different camera)
            cap = cv2.VideoCapture(cam)
            cv2.namedWindow(f"Camera {port_no}", cv2.WINDOW_NORMAL)
    
            start_time = time.time()
            frame_count = 0
    
            while True:
                ret, frame = cap.read()
                cv2.imshow(f"Camera {port_no}", frame)
    
                data = pickle.dumps(frame)
                msg_size = struct.pack("Q", len(data))
                client_socket.sendall(msg_size)
                client_socket.sendall(data)
    
                frame_count += 1
                if frame_count >= 10:
                    end_time = time.time()
                    fps = frame_count / (end_time - start_time)
                    #rint(f"Camera {port_no} - FPS: {fps:.2f}")
                    frame_count = 0
                    start_time = end_time
    
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            client_socket.close()
            server_socket.close()
    
    # Use a dictionary to store camera-port pairs
    camera_threads = {
        #11: 0,
        22: r"E:\movies\Untitled 16_1440p.mp4",
        #33: 2,
       #ff 44: 3,
    }
    
    threads = {}
    for port, cam in camera_threads.items():
        thread = threading.Thread(target=send_frames, args=(port, cam))
        threads[thread] = threads.get(thread,0)

        thread.start()
    thread = threading.Thread(target=message, args=(55,))
    threads[thread] = threads.get(thread,0)
    thread.start()
    
    for thread in threads.keys():
        thread.join()
    
camserver()
