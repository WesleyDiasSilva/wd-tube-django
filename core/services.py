class VideoService:
  def process_upload(self, video_id: int, chunk_index: int, bytes: bytes):
    print(f'Processing upload for video {video_id} chunk {chunk_index}...')