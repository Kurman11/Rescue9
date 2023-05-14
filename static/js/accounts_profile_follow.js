const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

form.addEventListener('submit', function (event) {
  event.preventDefault()
  const userId = event.target.dataset.userId
  
  axios({
    method: 'post',
    url: `/accounts/${userId}/follow/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      console.log(response.data.is_followed)
      const isFollowed = response.data.is_followed
      const followBtn = document.querySelector('#follow-form > input[type=submit]')
      console.log(followBtn)


      if (isFollowed === true) {
        followBtn.value = 'Unfollow'
      } else {
        followBtn.value = 'Follow'
      }

      const followingCountTag = document.querySelector('#followings-count')
      const followerCountTag = document.querySelector('#followers-count')

      console.log(followingCountTag)
      console.log(followerCountTag )

      const followingsCountData = response.data.followings_count
      const followersCountData = response.data.followers_count

      followingCountTag.textContent = followingsCountData
      followerCountTag.textContent = followersCountData
    })
})