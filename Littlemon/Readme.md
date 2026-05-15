"""# AXON - Modern Restaurant Management System

**AXON** is a full-stack Django web application designed to bridge the gap between restaurant customers and administrators. It features a dynamic menu, a smart reservation system with custom logic, and a dedicated management view for restaurant owners.

🚀 **Live Demo:** [AXON Live on Railway](https://axon404z.up.railway.app/)

---

## 👨‍💻 Author
**Mostafa Elhwary**  
GitHub: [@mostafa404z](https://github.com/mostafa404z)

---

## ✨ Features

The application consists of **7 specialized webpages**:

1.  **Home Page:** High-impact landing page introducing the AXON experience.
2.  **Authentication:** Secure Login and Account Creation systems for customers.
3.  **About Us:** Includes a functional **Feedback & Complaint Form**. Submissions are saved directly to the backend for administrative review.
4.  **Dynamic Menu:**
    *   **Category Filtering:** Users can view the full menu or filter by specific categories (JS-enhanced).
    *   **Cloudinary Integration:** Images are hosted on Cloudinary and linked to the backend, ensuring fast delivery.
    *   **No-Code Management:** Restaurant managers can add or modify menu items through the admin panel without touching any code.
5.  **Booking Page:** A smart table reservation system with built-in constraints:
    *   **Date Protection:** Users cannot book for a past date.
    *   **Capacity Logic:** A maximum of **50 people** can be booked for the same day to prevent overcapacity.
6.  **Reservations Page:**
    *   **Customer View:** Users see their own specific bookings.
    *   **Manager View:** Users with manager permissions can view all books across the system.
    *   **Auto-Expiry:** The system automatically marks past reservations as "Expired."
7.  **Protected Access:** The website is secured using **custom middleware** to manage access and protect routes.

---

## 🛠 Tech Stack

*   **Backend:** Django (Python)
*   **Frontend:** HTML5, CSS3, JavaScript
*   **Database:** [TiDB](https://www.pingcap.com/tidb-cloud/) (Distributed SQL for high performance)
*   **Media Hosting:** [Cloudinary](https://cloudinary.com/)
*   **Deployment:** Railway

---

## 🗄 Database & Performance Optimization

To overcome the storage and speed limitations of standard free-tier hosting, I implemented:

*   **TiDB Integration:** By linking the backend to a TiDB cluster, the application handles larger datasets and executes queries faster than standard storage limits on Railway or Render.
*   **Cloudinary Storage:** Using Cloudinary ensures that the heavy lifting of image hosting is offloaded, keeping the Django server lightweight and fast.
*   **Middleware:** Custom middleware ensures that only authorized users can interact with sensitive data.

---

## 🚀 Installation & Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/mostafa404z/LittleLemon.git

# 2. Enter the directory
cd LittleLemon

# 3. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate # On Windows use: venv\\Scripts\\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver