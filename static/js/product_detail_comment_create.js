const commentForm = document.querySelector('#comment-form')

commentForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const formData = new FormData(commentForm)

  axios({
    method: 'post',
    url: commentForm.getAttribute('action'),
    data: formData,
    headers: {'Content-Type': 'multipart/form-data'},
  })
    .then((response) => {
      location.reload();
    })
    .catch((error) => {
      console.log(error.response.data);
    })
})