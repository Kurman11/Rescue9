const forms = document.querySelectorAll(".like-form")
const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value

forms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault()
    const productId = event.target.dataset.productId
    axios ({
      method: 'post',
      url: `/products/${productId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })   
    .then((response) => {
      console.log(response)
      const isLiked = response.data.is_liked
      const likeBtn = form.querySelector(`#like-btn`)
      if (isLiked){
        likeBtn.className = 'bi bi-heart-fill'
      } else{
        likeBtn.className = 'bi bi-heart'
      }

      const likesCountTag = form.querySelector(`#like-count`)
      const likesCountData = response.data.like_count
      likesCountTag.textContent = likesCountData
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})
