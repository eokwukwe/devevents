import { test } from '@japa/runner'

import { UserFactory } from '#database/factories/user_factory'

test.group('Create User Resource', () => {
  test('validate required fields', async ({ client }) => {
    const res = await client.post('/users')

    res.assertStatus(422)
    res.assertBody({
      errors: {
        first_name: 'The first_name field is required',
        last_name: 'The last_name field is required',
        email: 'The email field is required',
        password: 'The password field is required',
      },
    })
  })

  test('validate email', async ({ client }) => {
    const res = await client.post('/users').json({
      email: 'foo',
      password: 'password',
      first_name: 'John',
      last_name: 'Doe',
    })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        email: 'The email field must be a valid email address',
      },
    })
  })

  test('validate email uniqueness', async ({ client }) => {
    const user = await UserFactory.create()

    const res = await client.post('/users').json({
      email: user.email,
      password: 'password',
      first_name: 'John',
      last_name: 'Doe',
    })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        email: 'The email has already been taken',
      },
    })
  })

  test('validate password length', async ({ client }) => {
    const res = await client.post('/users').json({
      email: 'some@mail.com',
      first_name: 'John',
      last_name: 'Doe',
      password: 'bar',
    })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        password: 'The password field must have at least 8 characters',
      },
    })
  })

  test('create user', async ({ client }) => {
    const res = await client.post('/users').json({
      email: 'some@mail.com',
      password: 'password',
      first_name: 'John',
      last_name: 'Doe',
    })

    res.assertStatus(201)
  })
})
