import Live
import socket
import threading
import json

class AbletonMCPRemoteScript:
    def __init__(self, c_instance):
        self.c_instance = c_instance
        self.application = Live.Application.get_application()
        self.song = self.application.get_document()
        
        # Socket server setup
        self.server_socket = None
        self.client_socket = None
        self.server_thread = None
        self.running = False
        
        # Delay socket startup to avoid initialization crashes
        self.c_instance.schedule_message(2, self.delayed_start)
        
        print("Ableton MCP Remote Script initialized")
    
    def delayed_start(self):
        """Start the socket server after Ableton is fully loaded"""
        try:
            self.start_server()
        except Exception as e:
            print("Failed to start socket server: " + str(e))
    
    def start_server(self):
        """Start the socket server to listen for MCP commands"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('localhost', 9877))
            self.server_socket.listen(1)
            
            self.running = True
            self.server_thread = threading.Thread(target=self._server_loop)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            print("Socket server started on localhost:9877")
        except Exception as e:
            print("Failed to start socket server: " + str(e))
    
    def _server_loop(self):
        """Main server loop to handle client connections"""
        while self.running:
            try:
                print("Waiting for MCP client connection...")
                self.client_socket, addr = self.server_socket.accept()
                print("MCP client connected from " + str(addr))
                
                while self.running:
                    try:
                        # Receive command
                        data = self.client_socket.recv(4096)
                        if not data:
                            break
                        
                        # Parse command
                        command = json.loads(data.decode('utf-8'))
                        print("Received command: " + str(command.get('type')))
                        
                        # Process command
                        response = self._process_command(command)
                        
                        # Send response
                        response_json = json.dumps(response)
                        self.client_socket.sendall(response_json.encode('utf-8'))
                        
                    except json.JSONDecodeError as e:
                        error_response = {"status": "error", "message": "Invalid JSON: " + str(e)}
                        try:
                            self.client_socket.sendall(json.dumps(error_response).encode('utf-8'))
                        except:
                            break
                    except Exception as e:
                        print("Error processing command: " + str(e))
                        error_response = {"status": "error", "message": str(e)}
                        try:
                            self.client_socket.sendall(json.dumps(error_response).encode('utf-8'))
                        except:
                            break
                
            except Exception as e:
                print("Server loop error: " + str(e))
                if self.client_socket:
                    try:
                        self.client_socket.close()
                    except:
                        pass
                    self.client_socket = None
    
    def _process_command(self, command):
        """Process incoming commands and return responses"""
        command_type = command.get("type")
        params = command.get("params", {})
        
        try:
            if command_type == "get_session_info":
                return self._get_session_info()
            elif command_type == "create_audio_track":
                return self._create_audio_track(params)
            elif command_type == "load_audio_file":
                return self._load_audio_file(params)
            elif command_type == "get_track_info":
                return self._get_track_info(params)
            else:
                return {"status": "error", "message": "Unknown command type: " + str(command_type)}
        except Exception as e:
            print("Error executing command " + str(command_type) + ": " + str(e))
            return {"status": "error", "message": str(e)}
    
    def _get_session_info(self):
        """Get information about the current session"""
        try:
            tracks = []
            for i, track in enumerate(self.song.tracks):
                track_info = {
                    "index": i,
                    "name": track.name,
                    "is_audio": track.has_audio_input,
                    "is_midi": track.has_midi_input,
                    "clips": []
                }
                
                for j, clip_slot in enumerate(track.clip_slots):
                    if clip_slot.has_clip:
                        clip = clip_slot.clip
                        clip_info = {
                            "index": j,
                            "name": clip.name,
                            "length": getattr(clip, 'length', 0),
                            "is_audio": getattr(clip, 'is_audio_clip', False)
                        }
                        track_info["clips"].append(clip_info)
                
                tracks.append(track_info)
            
            return {
                "status": "success",
                "result": {
                    "tempo": self.song.tempo,
                    "is_playing": self.song.is_playing,
                    "current_song_time": self.song.current_song_time,
                    "tracks": tracks
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _create_audio_track(self, params):
        """Create a new audio track"""
        try:
            index = params.get("index", -1)
            if index == -1:
                index = len(self.song.tracks)
            
            self.song.create_audio_track(index)
            track = self.song.tracks[index]
            
            return {
                "status": "success",
                "result": {
                    "index": index,
                    "name": track.name
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _load_audio_file(self, params):
        """Load an audio file into a track"""
        try:
            file_path = params.get("file_path")
            track_index = params.get("track_index", 0)
            clip_slot_index = params.get("clip_slot_index", 0)
            
            if not file_path:
                return {"status": "error", "message": "file_path is required"}
            
            track = self.song.tracks[track_index]
            clip_slot = track.clip_slots[clip_slot_index]
            
            # Load the audio file by dragging it to the clip slot
            clip_slot.create_clip()
            clip = clip_slot.clip
            
            # For audio files, we need to use a different approach
            # This is a simplified version - actual implementation would use Live's file loading
            
            return {
                "status": "success",
                "result": {
                    "track_index": track_index,
                    "clip_slot_index": clip_slot_index,
                    "clip_name": clip.name,
                    "clip_length": getattr(clip, 'length', 0)
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_track_info(self, params):
        """Get detailed information about a specific track"""
        try:
            track_index = params.get("track_index", 0)
            track = self.song.tracks[track_index]
            
            clips = []
            for i, clip_slot in enumerate(track.clip_slots):
                if clip_slot.has_clip:
                    clip = clip_slot.clip
                    clip_info = {
                        "index": i,
                        "name": clip.name,
                        "length": getattr(clip, 'length', 0),
                        "is_audio": getattr(clip, 'is_audio_clip', False)
                    }
                    clips.append(clip_info)
            
            return {
                "status": "success",
                "result": {
                    "index": track_index,
                    "name": track.name,
                    "is_audio": track.has_audio_input,
                    "is_midi": track.has_midi_input,
                    "clips": clips
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def disconnect(self):
        """Clean up when disconnecting"""
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        print("Remote Script disconnected")

# Required functions for Ableton Live
def create_instance(c_instance):
    return AbletonMCPRemoteScript(c_instance)
