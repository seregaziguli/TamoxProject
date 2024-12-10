from httpx import AsyncClient

async def test_register_user(ac: AsyncClient):
    response = await ac.post("/users", json={
      "name": "John Doa",
      "phone_number": "+1234567891",
      "email": "johndoe1@gmail.com",
      "password": "securepassword123"
    })
    
    assert response.status_code == 201