from flask import Blueprint, request, redirect, abort, url_for, send_from_directory
from pathlib import Path
from models.staffs import Staff
from flask_login import login_required, current_user
import os

staff_files = Blueprint("staff_files", __name__)

@staff_files.route("/staffs/<int:staff_id>/image/", methods=["POST"])
@login_required
def edit_file(staff_id):
    staff=Staff.query.get_or_404(staff_id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix != ".pdf":
            return abort(400, description="Invalid file type")
        image.save(f"/home/alexl/Project/my_app/my_app/static/{staff.image_filename}")
        return redirect(url_for("staffs.get_staff_member", staff_id=staff_id))
    return abort(400, description="No File")