$('.owl-carousel').owlCarousel({
  loop:true,
  margin:10,
  loop: false,
  responsive:{
      0:{
          items:2,
          slideBy:2,
      },
      600:{
          items:4,
          slideBy:4,
      },
      1000:{
          items:6,
          slideBy:6,
      },
  }
})