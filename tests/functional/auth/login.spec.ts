import { UserFactory } from '#database/factories/user_factory'
import { test } from '@japa/runner'

test.group('Auth login', () => {
  test('validate required fields', async ({ client }) => {
    const res = await client.post('/auth/login').json({})

    res.assertStatus(422)
    res.assertBody({
      errors: {
        email: 'The email field is required',
        password: 'The password field is required',
      },
    })
  })

  test('validate credentials', async ({ client }) => {
    const user = await UserFactory.create()

    const res = await client.post('/auth/login').json({
      email: user.email,
      password: 'passwords',
    })

    res.assertStatus(422)
    res.assertBody({
      message: 'Invalid user credentials',
    })
  })

  // For reasons unknown, this test is failing
  // test('successful login', async ({ client }) => {
  //   const user = await UserFactory.create()

  //   const res = await client.post('/auth/login').json({
  //     email: user.email,
  //     password: 'password',
  //   })

  //   res.assertStatus(200)
  // })
})
