const comment_like_forms = document.querySelectorAll('.comment_like_forms')
const r_csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
comment_like_forms.forEach(form => {
  form.addEventListener('submit', function (event) {  
    event.preventDefault()
    const productId = event.target.dataset.productId;
    const commentId = event.target.dataset.commentId;
    axios({
      method: 'post',
      url: `/products/${productId}/comments/${commentId}/comment_likes/`,
      headers: {'X-CSRFToken': r_csrfToken},
    })
    .then((response) => {
      const isLiked = response.data.r_is_like
      const likeBtn = document.querySelector(`#comment-like-btn-${commentId}`)
      if (isLiked){
        likeBtn.className = "bi bi-heart-fill title--likescount  btn m-0 p-0 fs-5"
      } else {likeBtn.className = "bi bi-heart title--likescount  btn m-0 p-0 fs-5"}

      const likesCountData = response.data.r_like_count
      console.log(response.data.r_like_count)  // 여기로 옮깁니다.
      const likesCountTag = document.querySelector(`#r_likes_count_${commentId}`)
      likesCountTag.textContent = likesCountData

      //location.reload();
    })
    .catch((error) => {
      console.error(response.data);
    });
  });
});