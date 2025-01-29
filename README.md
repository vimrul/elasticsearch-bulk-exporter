# elasticsearch-bulk-exporter
A simple and efficient tool to export large Elasticsearch datasets to JSON &amp; CSV, using the Scroll API with authentication support.

# 🚀 Elasticsearch Bulk Exporter

A **Python script** to efficiently **export large datasets** from **Elasticsearch** to **JSON and CSV**. Supports **authentication, pagination (Scroll API), and incremental writing**, making it suitable for handling millions of records.

---

## 🔹 Features
✔ **Exports Elasticsearch data to JSON & CSV**  
✔ **Handles large datasets using Scroll API** (prevents timeouts)  
✔ **Supports authentication (username & password)**  
✔ **Saves data incrementally** (avoids memory overload)  
✔ **Clears Scroll ID** to free Elasticsearch memory  
✔ **Live progress tracking** during export  

---

## 🔧 Requirements
Ensure you have **Python 3** and the required dependencies installed:

```sh
pip install requests
```

---

## 🚀 How to Use

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/elasticsearch-bulk-exporter.git
cd elasticsearch-bulk-exporter
```

### **2️⃣ Update Configuration**
Edit `export.py` and replace **Elasticsearch details** with your own:
```python
ES_URL = "http://your-elasticsearch-server:9200"
USERNAME = "your_username"
PASSWORD = "your_password"
INDEX = "filebeat-*"
```

### **3️⃣ Run the Export Script**
```sh
python export.py
```
This will:  
✅ Fetch records in **batches**  
✅ Write them **incrementally** to `export.json` and `export.csv`  
✅ Display **progress updates**  

---

## 📄 Example Output
```
Exported 5000 records so far...
Exported 10000 records so far...
Export completed successfully! Total records exported: 29729771
```

---

## 🛠️ Configuration Options
| Parameter       | Default Value        | Description |
|---------------|-----------------|-------------|
| `ES_URL`      | `"http://localhost:9200"` | Elasticsearch server URL |
| `USERNAME`    | `"your_username"` | Elasticsearch authentication username |
| `PASSWORD`    | `"your_password"` | Elasticsearch authentication password |
| `INDEX`       | `"filebeat-*"` | Elasticsearch index pattern |
| `size`        | `5000` | Number of records fetched per request (adjust for performance) |
| `scroll`      | `"5m"` | Scroll time to keep the search context active |

---

## 🛠️ Troubleshooting
**Q: Kibana shows a timeout (502 Bad Gateway). What should I do?**  
✔ Use the **Scroll API** instead of regular queries. This script handles that.  
✔ Reduce `"size": 5000` to `"size": 2000` to avoid memory overload.  

**Q: How do I export a different Elasticsearch index?**  
✔ Change the `INDEX` variable inside the script (`"filebeat-*"` → `"your_index-*"`).  

**Q: How do I run this script in the background?**  
✔ Use **nohup**:
```sh
nohup python export.py > export.log 2>&1 &
```
✔ Or use **screen**:
```sh
screen -S elasticsearch_export
python export.py
```
Press `CTRL+A` then `D` to **detach** from the session.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## ❤️ Contributing
Pull requests are welcome! If you find a bug or have an idea to improve the script, feel free to **open an issue** or submit a PR.

---

## 🌟 Support & Feedback
If this script helped you, please ⭐ **star the repository** and spread the word! 🚀

