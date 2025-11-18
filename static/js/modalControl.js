/* ==========================================================================
   MODAL CONTROLLER – Warung Football
   Handles Add, Edit, Delete modals with AJAX
   ========================================================================== */


// ---------- CSRF Helper ----------
function getCsrfToken() {
  const name = "csrftoken";
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));
  return cookie ? cookie.split("=")[1] : "";
}

/* =============================  EDIT PRODUCT  ============================ */

let editTargetId = null;

window.openEditModal = async function (productId) {
  editTargetId = productId;
  const modal = document.getElementById("editModal");
  if (!modal) {
    alert("Missing editModal HTML in base.html");
    return;
  }

  modal.classList.remove("hidden");

  try {
    const res = await fetch(`/json/${productId}/`);
    if (!res.ok) throw new Error(`Status ${res.status}`);
    const data = await res.json();

    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.value = val;
    };

    set("editProductId", data.id || productId);
    set("editProductName", data.name || "");
    set("editProductPrice", data.price || 0);
    set("editProductDesc", data.descriptions || "");
    set("editProductThumb", data.thumbnail || "");
    set("editProductCategory", data.category || "");

    if (typeof showToast === "function")
      showToast("Loaded", "Product data ready for editing", "success");
  } catch (err) {
    console.error("Edit Load Error:", err);
    if (typeof showToast === "function")
      showToast("Error", "Could not load product data", "error");
  }
};

window.closeEditModal = function () {
  const modal = document.getElementById("editModal");
  if (modal) modal.classList.add("hidden");
  editTargetId = null;
};

/* Submit update */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("editProductForm");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!editTargetId) return;

    const data = {};
    form.querySelectorAll("input, textarea, select").forEach((i) => {
      data[i.name] = i.value;
    });

    try {
      const res = await fetch(`/product/${editTargetId}/edit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(data),
      });

      if (res.ok) {
        closeEditModal();
        document.dispatchEvent(new CustomEvent("productUpdated"));
        if (typeof showToast === "function")
          showToast("Success", "Product updated", "success");
      } else throw new Error(`Status ${res.status}`);
    } catch (err) {
      console.error("Submit error:", err);
      if (typeof showToast === "function")
        showToast("Error", "Update failed", "error");
    }
  });
});

/* =============================  DELETE PRODUCT  ============================ */

let deleteTargetId = null;

window.openDeleteModal = function (productId, productName) {
  deleteTargetId = productId;
  const modal = document.getElementById("deleteModal");
  const nameSpan = document.getElementById("deleteProductName");
  if (nameSpan) nameSpan.textContent = productName;
  if (modal) modal.classList.remove("hidden");
};

window.closeDeleteModal = function () {
  const modal = document.getElementById("deleteModal");
  if (modal) modal.classList.add("hidden");
  deleteTargetId = null;
};

document.addEventListener("DOMContentLoaded", () => {
  const confirm = document.getElementById("confirmDeleteBtn");
  if (!confirm) return;

  confirm.addEventListener("click", async () => {
    if (!deleteTargetId) return;
    try {
      const res = await fetch(`/product/${deleteTargetId}/delete/`, {
        method: "POST",
        headers: { "X-CSRFToken": getCsrfToken() },
      });

      if (res.ok) {
        closeDeleteModal();
        document.dispatchEvent(new CustomEvent("productDeleted"));
        if (typeof showToast === "function")
          showToast("Success", "Product deleted", "success");
      } else throw new Error(res.status);
    } catch (err) {
      console.error("Delete error:", err);
      if (typeof showToast === "function")
        showToast("Error", "Failed to delete", "error");
    }
  });
});

/* ===============================  ADD PRODUCT  ============================ */

window.openProductModal = function () {
  document.getElementById("productModal")?.classList.remove("hidden");
};

window.closeProductModal = function () {
  document.getElementById("productModal")?.classList.add("hidden");
};

window.addProductEntry = async function () {
  const form = document.getElementById("productForm");
  if (!form) return false;

  try {
    const res = await fetch("/add_product_entry_ajax/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
      body: new FormData(form),
    });
    if (!res.ok) throw new Error("Failed to add");
    form.reset();
    closeProductModal();
    document.dispatchEvent(new CustomEvent("productAdded"));
    if (typeof showToast === "function")
      showToast("Success", "Product added", "success");
  } catch (err) {
    console.error("Add error:", err);
    if (typeof showToast === "function")
      showToast("Error", "Add product failed", "error");
  }
  return false;
};

document.addEventListener("DOMContentLoaded", () => {
  const addForm = document.getElementById("productForm");
  if (addForm) {
    addForm.addEventListener("submit", (e) => {
      e.preventDefault();
      addProductEntry();
    });
  }
});

console.log("=== MODALCONTROL READY ===");