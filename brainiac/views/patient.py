from bson.binary import Binary
import io
from flask import Blueprint, render_template, url_for, current_app, request, session
import time

patient_bp = Blueprint("patient", __name__, url_prefix="/patient")


@patient_bp.route("/dashboard")
def dashboard():

    patient_data = current_app.db.patients.find_one(
        {'user_id': session['user_id']})

    if patient_data is None:
        return "No patient found", 404

    if "scans" in patient_data:
        # Retrieve image URLs from the MongoDB document
        print(patient_data['scans'])
        return render_template('patient_dash.html', patient=patient_data, cases=patient_data['scans'])
    else:
        return render_template('patient_dash.html', patient=patient_data, image_urls=[])

    # patient_data = current_app.db.patients.find_one(
    #     {"user_id": session["user_id"]})

    # # list all the blobs in the container
    # blob_items = current_app.container_client.list_blobs()

    # img_html = ""

    # for blob in blob_items:
    #     # get blob client to interact with the blob and get blob url
    #     blob_client = current_app.container_client.get_blob_client(
    #         blob=blob.name)
    #     # get the blob url and append it to the html
    #     # img_html += "<img src="{}" width="auto" height="200"/>".format( blob_client.url)
    #     img_html += blob_client.url + " "
    # print("img_html: ", img_html)
    # if patient_data is None:
    #     return "No patient found", 404

    # # Define the paths to your images
    image_paths = [url_for("static", filename="images/case-1.jpg"),
                   url_for("static", filename="images/case-2.png")]
    return render_template("patient_dash.html", patient=patient_data, image_paths=image_paths)


@patient_bp.route("/dashboard", methods=["POST"])
def upload_image():
    if request.method == "POST":
        scan_names = []
        img_count = 1
        img_urls = []
        patient_id = session["user_id"]
        patient_data = current_app.db.patients.find_one(
            {"user_id": session["user_id"]})

        case_count = 1
        # check if case number exists
        if "case_number" in patient_data:
            case_count = patient_data["case_number"] + 1

        # update azure
        for scan in request.files.getlist("scans"):
            try:
                # rename file
                new_scan_name = "patient" + \
                    str(patient_id) + "_" + "case" + \
                    str(case_count) + "_" + "img" + str(img_count)
                img_count += 1
                print(new_scan_name)
                scan_names.append(new_scan_name)

                # upload image and get url
                blob_client = current_app.container_client.get_blob_client(
                    new_scan_name)
                current_app.container_client.upload_blob(new_scan_name, scan)
                img_urls.append(blob_client.url)
                # filenames += scan.filename + " " + new_scan_name + "<br /> "
            except Exception as e:
                print(e)
                # ignore duplicate filenames
                print("Ignoring duplicate filenames")

        # update mongodb
        case_name = "case" + str(case_count)
        current_app.db.patients.update_one(
            {"user_id": patient_id},
            {
                "$set": {"scans." + case_name: img_urls},
                "$inc": {"case_number": 1}
            }
        )

        # current_app.db.patients.update_one(
        #     {"patient_id": patient_id},
        #     {"$set": {"scans." + case_name: scan_names}},
        #     upsert=True)

        return "<p>Uploaded: <br />{}</p>".format(scan_names)

        # for file in request.files.getlist("scans"):
        #     try:
        #         # file.filename += patient_id
        #         current_app.container_client.upload_blob(
        #             file.filename, file)
        #         scan_names.append(file.filename)
        #     except Exception as e:
        #         print(e)
        #         # ignore duplicate filenames
        #         print("Ignoring duplicate filenames")

        # patient_id = session["user_id"]
        # case_name = "case"
        # current_app.db.patients.update_one(
        #     {"patient_id": patient_id},
        #     {"$set": {"scans." + case_name: scan_names}},
        #     upsert=True)

        #     return "MRI scans uploaded and added to patient"s case successfully!"
        # else:
        #     return "No MRI scans uploaded!", 400
