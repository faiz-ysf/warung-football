// ===========================================================
//  GLOBAL MODAL CONTROLLER for Warung Football
// ===========================================================

// ---------- CSRF Helper ----------
function getCsrfToken() {
  const name = "csrftoken";
  const cookie = document.cookie
    .split("; ")
    .find((row) => row.startsWith(name + "="));
  return cookie ? cookie.split("=")[1] : "";
}

// ===========================================================
// DELETE MODAL
// ===========================================================
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
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener("click", async () => {
      if (!deleteTargetId) return;
      try {
        const deleteUrl = `/product/${deleteTargetId}/delete/`;
        const res = await fetch(deleteUrl, {
          method: "POST",
          headers: { "X-CSRFToken": getCsrfToken() },
        });
        if (res.ok) {
          closeDeleteModal();
          document.dispatchEvent(new CustomEvent("productDeleted"));
        } else {
          alert("Failed to delete product");
        }
      } catch (err) {
        console.error("Delete error:", err);
      }
    });
  }
});

// ===========================================================
// EDIT MODAL
// ===========================================================
let editTargetId = null;

window.openEditModal = function (productId) {
  editTargetId = productId;
  const modal = document.getElementById("editModal");
  const product = window.allProducts
    ? window.allProducts.find((p) => p.id === productId)
    : null;

  if (!modal || !product) return;

  document.getElementById("editProductId").value = product.id;
  document.getElementById("editProductName").value = product.name;
  document.getElementById("editProductPrice").value = product.price;
  document.getElementById("editProductDesc").value = product.descriptions;
  document.getElementById("editProductThumb").value = product.thumbnail || "";
  document.getElementById("editProductCategory").value = product.category;

  modal.classList.remove("hidden");
};

window.closeEditModal = function () {
  const modal = document.getElementById("editModal");
  if (modal) modal.classList.add("hidden");
  editTargetId = null;
};

document.addEventListener("DOMContentLoaded", () => {
  const editForm = document.getElementById("editProductForm");
  if (editForm) {
    editForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (!editTargetId) return;
      const formData = {
        name: document.getElementById("editProductName").value,
        price: document.getElementById("editProductPrice").value,
        descriptions: document.getElementById("editProductDesc").value,
        thumbnail: document.getElementById("editProductThumb").value,
        category: document.getElementById("editProductCategory").value,
      };
      try {
        const editUrl = `/product/${editTargetId}/edit`;
        const res = await fetch(editUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify(formData),
        });
        if (res.ok) {
          closeEditModal();
          document.dispatchEvent(new CustomEvent("productUpdated"));
        } else {
          alert("Failed to update product");
        }
      } catch (err) {
        console.error("Edit error:", err);
      }
    });
  }
});

// ===========================================================
// ADD PRODUCT MODAL (reuses the one in modal.html)
// ===========================================================
window.openProductModal = function () {
  document.getElementById("productModal")?.classList.remove("hidden");
};

window.closeProductModal = function () {
  document.getElementById("productModal")?.classList.add("hidden");
};

window.addProductEntry = async function () {
  try {
    const form = document.querySelector("#productForm");
    const res = await fetch("/add_product_entry_ajax/", {
      method: "POST",
      body: new FormData(form),
    });
    if (!res.ok) throw new Error("Failed to add product");
    form.reset();
    closeProductModal();
    document.dispatchEvent(new CustomEvent("productAdded"));
  } catch (err) {
    console.error("Add error:", err);
  }
  return false;
};

document.addEventListener("DOMContentLoaded", () => {
  const addForm = document.getElementById("productForm");
  if (addForm) {
    addForm.addEventListener("submit", function (e) {
      e.preventDefault();
      addProductEntry();
    });
  }
});