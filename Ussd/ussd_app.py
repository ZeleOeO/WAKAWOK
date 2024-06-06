from flask import Flask, request
import os

app = Flask(__name__)


def create_profile(name, job, contact, phone):
    profile = {"name": name, "job": job, "contact": contact, "phone": phone}
    return "Profile created successfully."


def get_profiles():
    profiles = [
        {"name": "John Doe", "job": "Mechanic"},
        {"name": "Jane Smith", "job": "Plumber"},
    ]
    return profiles


@app.route("/", methods=["POST"])
def ussd_callback():
    session_id = request.form.get("sessionId")
    service_code = request.form.get("serviceCode")
    phone_number = request.form.get("phoneNumber")
    text = request.form.get("text")

    response_text = ""

    if text == "":
        response_text = "Welcome to the WAKAWOK USSD App.\nSelect a language:\n1. English\n2. Yoruba"
    elif text == "1":
        response_text = "Enter your name:"
    elif text == "2":
        response_text = "Kọ orukọ rẹ: "
    elif text.startswith("1*"):
        steps = text.split("*")
        if len(steps) == 2:
            response_text = "Enter your work:"
        elif len(steps) == 3:
            response_text = "Enter your contact email:"
        elif len(steps) == 4:
            response_text = "Enter your phone number:"
        elif len(steps) == 5:
            name, job, contact, phone = steps[1:]
            response_text = create_profile(name, job, contact, phone)
    elif text.startswith("2*"):
        steps = text.split("*")
        if len(steps) == 2:
            response_text = "Kini iṣẹ rẹ:"
        elif len(steps) == 3:
            response_text = "Fọwọsi ẹẹ imeeli oṣu rẹ:"
        elif len(steps) == 4:
            response_text = "Kini nọmba foonu rẹ:"
        elif len(steps) == 5:
            name, job, contact, phone = steps[1:]
            response_text = create_profile(name, job, contact, phone)
    elif text == "3":
        profiles = get_profiles()
        if profiles:
            response_text = "Here are the available profiles:\n"
            for i, profile in enumerate(profiles, start=1):
                response_text += f"{i}. {profile['name']} - {profile['job']}\n"
        else:
            response_text = "No profiles available."
    else:
        response_text = "Invalid input. Please try again."

    return f"CON {response_text}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
