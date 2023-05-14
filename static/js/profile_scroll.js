document.addEventListener('DOMContentLoaded', function() {
  const profileBox = document.getElementById('profile-box');

  
  window.addEventListener('scroll', function() {
    const scrollY = window.scrollY;
    
    if(window.innerWidth > 768) {
      profileBox.style.top = `${scrollY}px`;
    } 
  });
});
