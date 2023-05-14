const profileBox = document.getElementById('profile-box');
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  profileBox.style.top = `${scrollY}px`;
});
