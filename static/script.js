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

  // Remove fade animation
  document.body.classList.remove('fade');
};

// Smooth transition on internal link clicks
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

  // Handle touch events for theme toggle on mobile
  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('touchstart', function (e) {
      e.preventDefault();
      toggleDarkMode();
    });
  }

  // Client-side form validation for home.html
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function (e) {
      const readingScore = document.querySelector('input[name="reading_score"]');
      const writingScore = document.querySelector('input[name="writing_score"]');
      if (readingScore && (readingScore.value < 0 || readingScore.value > 100)) {
        e.preventDefault();
        readingScore.classList.add('shake');
        setTimeout(() => readingScore.classList.remove('shake'), 500);
        alert('Reading score must be between 0 and 100.');
      }
      if (writingScore && (writingScore.value < 0 || writingScore.value > 100)) {
        e.preventDefault();
        writingScore.classList.add('shake');
        setTimeout(() => writingScore.classList.remove('shake'), 500);
        alert('Writing score must be between 0 and 100.');
      }
    });
  }
});
