// JS to show loader during scan
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('scanForm');
  const loader = document.getElementById('loader');

  form.addEventListener('submit', function () {
    loader.style.display = 'block';
  });
});
