from flask import Blueprint, request, redirect, abort, url_for, send_from_directory
from pathlib import Path
from models.staffs import Staff
import os

staff_images = Blueprint("staff_images", __name__)

@staff_images.route("/staffs/<int:staff_id>/image/", methods=["POST"])
def update_image(staff_id):
    staff = Staff.query.get_or_404(staff_id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix != ".pdf":
            return abort(400, description="Invalid file type")
        image.save(f"my_app/static/{staff.image_filename}")
        return redirect(url_for("staffs.get_staff", staff_id=staff_id))
    return abort(400, description="No files attached")
