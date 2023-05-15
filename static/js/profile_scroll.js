
const profileBox = document.getElementById('profile-box');
window.addEventListener('scroll', () => {
  const scrollY = window.scrollY;
  if(window.innerWidth>768){
    profileBox.style.top = `${scrollY}px`;
  }
