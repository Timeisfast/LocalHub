// 백엔드 주소 환경변수에서 가져오기 (Day 1 .env에 세팅했던 것!)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const boardService = {
  // 1. 전체 게시글 목록 조회
  async getPosts() {
    const response = await fetch(`${API_BASE_URL}/api/posts`);
    if (!response.ok) throw new Error('목록 조회 실패');
    return response.json();
  },

  // 2. 개별 게시글 상세 조회
  async getPostById(id) {
    const response = await fetch(`${API_BASE_URL}/api/posts/${id}`);
    if (!response.ok) throw new Error('상세 조회 실패');
    return response.json();
  },

  // 3. 게시글 작성 (POST)
  async createPost(postData) {
    const response = await fetch(`${API_BASE_URL}/api/posts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    });
    if (!response.ok) throw new Error('게시글 작성 실패');
    return response.json();
  },

  // 4. 게시글 수정 (PUT)
  async updatePost(id, postData) {
    const response = await fetch(`${API_BASE_URL}/api/posts/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    });
    if (!response.ok) throw new Error('게시글 수정 실패');
    return response.json();
  },

  // 5. 게시글 삭제 (DELETE)
  async deletePost(id) {
    const response = await fetch(`${API_BASE_URL}/api/posts/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('게시글 삭제 실패');
    return response.json();
  }
};