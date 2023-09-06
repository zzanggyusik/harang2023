from PIL import Image
import os

class ImageManager():
    def convert_tif_to_jpeg(self, input_path, output_path):
        try:
            # .tif 이미지 열기
            with Image.open(input_path) as im:
                # JPEG 형식으로 저장
                im = im.convert("RGB")
                im.save(output_path, "JPEG")
                
            print(f"{input_path}를 {output_path}로 성공적으로 변환했습니다.")
            os.remove(input_path)
            
        except Exception as e:
            print(f"오류 발생: {e}")
            
if __name__ == "__main__":
    # 입력 및 출력 파일 경로 설정
    input_file = "./static/images/Image158_20230906121324.tif"  # .tif 파일의 경로
    output_file = "./static/images/Image158_20230906121324.jpeg"  # .jpeg로 변환한 이미지의 저장 경로

    # .tif를 .jpeg로 변환
    ImageManager().convert_tif_to_jpeg(input_file, output_file)
            