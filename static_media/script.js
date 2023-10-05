
const expand_btn = document.querySelector(".expand-btn");

let activeIndex;

expand_btn.addEventListener("click", () => {
  const iconImage = expand_btn.querySelector('img');

  document.body.classList.toggle("collapsed");
});

const current = window.location.href;

const allLinks = document.querySelectorAll(".sidebar-links a")

allLinks.forEach((elem) => {
  elem.addEventListener('click', function() {
    const hrefLinkClick = elem.href;

    allLinks.forEach((link) => {
      if (link.href == hrefLinkClick){
        link.classList.add("active");
      } else {
        link.classList.remove('active');
      }
    });
  })
});



let loginForm = document.querySelector(".my-form");
let email = document.getElementById("email");
let password = document.getElementById("password");
let confirmPassword = document.getElementById("confirm-password")

loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    console.log('Email:', email.value);
    console.log('Password:', password.value);
});

function onChange() {
    if (confirmPassword.value === password.value) {
        confirmPassword.setCustomValidity('');
    } else {
        confirmPassword.setCustomValidity('Passwords do not match!');
    }
}

password.addEventListener('change', onChange);
confirmPassword.addEventListener('change', onChange);



function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const showPasswordIcon = document.querySelector('.show-password');
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        showPasswordIcon.innerHTML = '&#128064;';  // Show hide icon
    } else {
        passwordField.type = 'password';
        showPasswordIcon.innerHTML = '&#128065;';  // Show hide icon
    }
}


const menuLink = document.querySelector('.link');
const submenu = document.querySelector('.submenu');

menuLink.addEventListener('click', () => {
    submenu.style.display = (submenu.style.display === 'none' || submenu.style.display === '') ? 'block' : 'none';
});

// function updateDataTable(data) {
//   // Assuming you have a DataTable initialized with ID 'foodItemsDataTable'
//   var table = $('#foodItemsDataTable').DataTable();

//   // Clear existing rows
//   table.clear();

//   // Add the new data to the table
//   data.forEach(function(item) {
//     table.row.add([
//       item.id,
//       item.name,
//       item.price,
//       item.is_available,
//       // ... Add action column content here ...
//     ]).draw(false);
//   });
// }

// // ... Rest of your JavaScript code ...

// document.getElementById('allFoodItemsLink').addEventListener('click', function(e) {
//   e.preventDefault();

//   // Increment the 'draw' parameter each time we make a request
//   var table = $('#foodItemsDataTable').DataTable();
//   var draw = table.page.info().draw + 1;

//   // Make an AJAX request to fetch the data for the data table
//   fetch('{% url "ajax_datatable_food_items_list" %}?draw=' + draw)  // Include the 'draw' parameter
//     .then(response => response.json())
//     .then(data => {
//       // Assuming you have a function to update the data table with the fetched data
//       updateDataTable(data);
//     })
//     .catch(error => console.error('Error fetching data:', error));
// });

$(document).ready(function() {
  var table = $('#foodItemsDataTable').DataTable({
      // DataTable options
      columns: [
          { data: 'id', title: 'ID' },
          { data: 'name', title: 'Name' },
          { data: 'price', title: 'Price' },
          { data: 'is_available', title: 'Available' },
          {
              data: null,
              render: function(data, type, row) {
                  return `
                      <td class="text-end">
                          <a href="#" class="btn btn-light btn-active-light-primary btn-sm" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Actions
                              <span class="svg-icon svg-icon-5 m-0">
                                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                      <path d="M11.4343 12.7344L7.25 8.55005C6.83579 8.13583 6.16421 8.13584 5.75 8.55005C5.33579 8.96426 5.33579 9.63583 5.75 10.05L11.2929 15.5929C11.6834 15.9835 12.3166 15.9835 12.7071 15.5929L18.25 10.05C18.6642 9.63584 18.6642 8.96426 18.25 8.55005C17.8358 8.13584 17.1642 8.13584 16.75 8.55005L12.5657 12.7344C12.2533 13.0468 11.7467 13.0468 11.4343 12.7344Z" fill="currentColor"></path>
                                  </svg>
                              </span>
                          </a>
                          <div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4" data-kt-menu="true" style="">
                              <div class="menu-item px-3">
                                  <a href="${data.action}" class="menu-link px-3">Edit</a>
                              </div>
                          </div>
                      </td>
                  `;
              }
          }
      ]
  });

  $('#allFoodItemsLink').click(function(e) {
      e.preventDefault();
      fetchFoodItemsData(table);
  });

  function fetchFoodItemsData(table) {
      fetch('{% url "ajax_datatable_food_items_list" %}')
          .then(response => response.json())
          .then(data => {
              table.clear();
              table.rows.add(data).draw();
          })
          .catch(error => console.error('Error fetching data:', error));
  }
});

document.getElementById("addFoodItemBtn").addEventListener("click", function() {
  window.location.href = "{% url 'add_food_item_page' %}";
});