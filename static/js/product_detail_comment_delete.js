const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
function deleteComment(event, product_pk, comment_pk) {
  event.preventDefault();
  if (confirm('댓글을 삭제하시겠습니까?')) {
    fetch(`/products/${product_pk}/comments/${comment_pk}/comment_delete/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('서버 에러');
      }
    })
    .then(data => {
      if (data.status === 'ok') {
        // Reload the page to reflect the updated comments
        location.reload();
      } else {
        alert(data.message);
      }
    })
    .catch(error => {
      alert(error.message);
    });
  }
}