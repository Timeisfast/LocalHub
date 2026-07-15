import api from './index'

export const postApi = {
  // 전체 게시글 조회
  getPosts() {
    return api.get('/posts/')
  },
  // 게시글 작성
  createPost(postData) {
    return api.post('/posts/', postData)
  },
  // 단건 게시글 상세 조회
  getPostDetail(postId) {
    return api.get(`/posts/${postId}`)
  },
  // 게시글 수정
  updatePost(postId, postData) {
    return api.put(`/posts/${postId}`, postData)
  },
  // 게시글 삭제
  deletePost(postId, password) {
    return api.delete(`/posts/${postId}`, {
      params: { password }
    })
  },
  // 게시글 검색
  searchPosts(keyword) {
    return api.get('/posts/search', {
      params: { keyword }
    })
  },
  // 게시글 페이징 조회
  getPostsPage(page = 1, size = 10) {
    return api.get('/posts/page', {
      params: { page, size }
    })
  },
  // 게시글 비밀번호 검증
  verifyPostPassword(postId, password) {
    return api.post(`/posts/${postId}/verify`, { password })
  }
}

export const placeApi = {
  // 관광지/쇼핑 목록 조회 (category: 'tourist' | 'shopping')
  getPlaces(category) {
    return api.get('/places/', {
      params: { category }
    })
  },
  // 상세 장소 정보 조회
  getPlaceDetail(placeId, category) {
    return api.get(`/places/${placeId}`, {
      params: { category }
    })
  }
}

export const festivalApi = {
  // 축제 일정 리스트 조회
  getFestivals() {
    return api.get('/events/')
  },
  // 개별 축제 상세 조회
  getFestivalDetail(eventId) {
    return api.get(`/events/${eventId}`)
  }
}