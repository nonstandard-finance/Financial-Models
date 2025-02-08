import qrcode
import uuid
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import base64
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException


from app.core.constants import BUCKET_NAME
from app.core.storage import s3_client


def generate_qr_code(data: str) -> Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img


def overlay_qr_code(
    badge_image_url: str, qr_code: Image, user_name: str, user_ens_domain: str = None
) -> dict:
    badge_image = Image.open(requests.get(badge_image_url, stream=True).raw)
    qr_code_size = (
        badge_image.width // 4,
        badge_image.height // 4,
    )  # QR code is 1/16 the size of the image
    qr_code = qr_code.resize(qr_code_size)

    badge_image.paste(
        qr_code,
        (
            badge_image.width - qr_code_size[0] - 10,
            badge_image.height - qr_code_size[1] - 10,
        ),
    )  # Adjust position

    draw = ImageDraw.Draw(badge_image)
    font_size = (
        badge_image.height // 16
    )  # Username or ENS domain is 3/16 the size of the image
    font = ImageFont.truetype("arial.ttf", font_size)

    display_name = user_ens_domain if user_ens_domain else user_name
    draw.text((10, 10), display_name, fill="black", font=font)

    buffer = BytesIO()
    badge_image.save(buffer, format="PNG")
    image_bytes = buffer.getvalue()

    s3_key = f"badges/{user_name}/{uuid.uuid4()}.png"
    try:
        s3_client.put_object(
            Bucket=BUCKET_NAME, Key=s3_key, Body=image_bytes, ContentType="image/png"
        )
        s3_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return {
            "s3_url": s3_url,
            "image_bytes": f"data:image/png;base64,{base64.b64encode(image_bytes).decode()}",
        }
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except PartialCredentialsError:
        raise HTTPException(status_code=500, detail="Incomplete AWS credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
