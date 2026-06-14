let cart = JSON.parse(localStorage.getItem("cart")) || [];

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartCount();
}

document.addEventListener("DOMContentLoaded", () => {

    const buttons =
        document.querySelectorAll(".ajax-cart-btn");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            const id =
                button.dataset.id;

            fetch(`/ajax/add/${id}/`)
                .then(response => response.json())
                .then(data => {

                    document.getElementById(
                        "cart-count"
                    ).innerText =
                        data.cart_count;

                    const toast =
                        document.getElementById(
                            "toast"
                        );

                    toast.classList.add("show");

                    setTimeout(() => {
                        toast.classList.remove("show");
                    }, 2000);

                });

        });

    });

});

document.addEventListener("DOMContentLoaded", () => {

    const menuToggle =
        document.getElementById("menu-toggle");

    const mobileMenu =
        document.getElementById("mobile-menu");

    if(menuToggle){

        menuToggle.addEventListener("click", () => {

            mobileMenu.classList.toggle(
                "show-menu"
            );

        });

    }

});

function addToCart(name, price) {
  cart.push({ name, price });
  saveCart();
  alert(name + " added to cart");
}

function updateCartCount() {
  const count = document.getElementById("cartCount");
  if (count) count.innerText = cart.length;
}

function toggleMenu() {
  document.getElementById("navMenu").classList.toggle("show");
}

function renderCart() {
  const container = document.getElementById("cartItems");
  if (!container) return;

  container.innerHTML = "";

  let total = 0;

  cart.forEach((item, index) => {
    total += item.price;

    container.innerHTML += `
      <div class="card">
        <p>${item.name}</p>
        <strong>$${item.price}</strong>
        <button onclick="removeItem(${index})">Remove</button>
      </div>
    `;
  });

  document.getElementById("totalPrice").innerText = "Total: $" + total;
}

function removeItem(index) {
  cart.splice(index, 1);
  saveCart();
  renderCart();
}

function clearCart() {
  cart = [];
  saveCart();
  renderCart();
}

document.addEventListener("DOMContentLoaded", () => {
  updateCartCount();
  renderCart();
});

const slides =
document.querySelectorAll(".slide");

let current = 0;

function nextSlide(){

    slides[current].classList.remove("active");

    current++;

    if(current >= slides.length){
        current = 0;
    }

    slides[current].classList.add("active");
}

setInterval(nextSlide,4000);