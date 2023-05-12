const forms = document.querySelectorAll(".like-form")
const csrftokenLike = document.querySelector("[name=csrfmiddlewaretoken]").value

forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault()
    const productId = e.target.dataset.productId
    axios({
      method: 'post',
      url: `/products/${productId}/likes/`,
      headers: { "X-CSRFToken": csrftokenLike},
    }).then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = form.querySelector(`#like-btn`)
      if (isLiked){
        likeBtn.className = 'bi bi-heart-fill title--likescount btn p-0 m-0'
      } else{
        likeBtn.className = 'bi bi-heart title--likescount btn p-0 m-0'
      }

      const likeCountTag = form.querySelector('#like-count')
      const likeCountData = response.data.like_count
      likeCountTag.textContent = likeCountData
    })
    .catch((error) => {
      console.log(error.response)
    })
  })
})
