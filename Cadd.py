from flask import Flask, request, send_file, jsonify
import csv
import os

temp_dir = "temp/"
os.makedirs(temp_dir, exist_ok=True)

app = Flask(__name__)

def save_csv(contacts, filename="contacts.csv"):
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone Number", "Email"])  # Header
        for contact in contacts:
            writer.writerow([contact["name"], contact["phone"], contact.get("email", "")])
    return filepath

def save_tsv(contacts, filename="contacts.tsv"):
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["Name", "Phone Number", "Email"])
        for contact in contacts:
            writer.writerow([contact["name"], contact["phone"], contact.get("email", "")])
    return filepath

def save_vcf(contacts, filename="contacts.vcf"):
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        for contact in contacts:
            file.write("BEGIN:VCARD\n")
            file.write("VERSION:3.0\n")
            file.write(f"FN:{contact['name']}\n")
            file.write(f"TEL:{contact['phone']}\n")
            if contact.get("email"):
                file.write(f"EMAIL:{contact['email']}\n")
            file.write("END:VCARD\n\n")
    return filepath

@app.route("/generate", methods=["POST"])
def generate_contacts():
    data = request.json
    contacts = data.get("contacts", [])
    file_type = data.get("file_type", "csv")
    
    if not contacts:
        return jsonify({"error": "No contacts provided"}), 400
    
    if file_type == "csv":
        filepath = save_csv(contacts)
    elif file_type == "tsv":
        filepath = save_tsv(contacts)
    elif file_type == "vcf":
        filepath = save_vcf(contacts)
    else:
        return jsonify({"error": "Invalid file type"}), 400
    
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
