// Alinhado com backend: auth/schemas.py → UserOut, TokenResponse

export interface User {
  id: string
  name: string
  email: string
  photo_url: string | null
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  has_profile: boolean
}
