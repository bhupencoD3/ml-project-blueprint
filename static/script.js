


// Toggle dark mode and save preference
function toggleDarkMode() {
  const isDark = document.body.classList.toggle('dark-mode');
  localStorage.setItem('darkMode', isDark);
  document.getElementById('theme-icon').textContent = isDark ? '🌞' : '🌙';
}

// Restore dark mode on page load
window.onload = () => {
  const isDark = localStorage.getItem('darkMode') === 'true';
  if (isDark) {
    document.body.classList.add('dark-mode');
    document.getElementById('theme-icon').textContent = '🌞';
  } else {
    document.getElementById('theme-icon').textContent = '🌙';
  }

  // Remove any fade animation if added
  document.body.classList.remove('fade');
};

// Optional: smooth transition on internal link clicks
document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('fade');

  const links = document.querySelectorAll('a[href]:not([target="_blank"])');
  links.forEach(link => {
    link.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (!href.startsWith('http') && !href.startsWith('#')) {
        e.preventDefault();
        document.body.classList.add('fade');
        setTimeout(() => {
          window.location.href = href;
        }, 300);
      }
    });
  });
});
