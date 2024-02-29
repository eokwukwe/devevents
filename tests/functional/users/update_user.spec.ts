import { test } from '@japa/runner'

import { UserFactory } from '#database/factories/user_factory'
import User from '#models/user/index'

test.group('Update User Resource', (group) => {
  let user1: User
  let user2: User

  group.setup(async () => {
    user1 = await UserFactory.create()
    user2 = await UserFactory.create()
  })

  test('check that user is authenticated', async ({ client }) => {
    const res = await client.put(`/users/${user1.id}`).json({})

    res.assertStatus(401)
    res.assertBody({ message: 'Unauthorized access' })
  })

  test('ensure user can only update their data', async ({ client }) => {
    const res = await client.put(`/users/${user1.id}`).loginAs(user2).json({})

    res.assertStatus(403)
    res.assertBody({ message: 'Unauthorized access' })
  })

  test('validate required fields', async ({ client }) => {
    const res = await client.put(`/users/${user1.id}`).loginAs(user1).json({})

    res.assertStatus(422)
    res.assertBody({
      errors: {
        bio: 'The bio field is required',
        email: 'The email field is required',
        first_name: 'The first_name field is required',
        last_name: 'The last_name field is required',
      },
    })
  })

  test('update user', async ({ client }) => {
    const res = await client.put(`/users/${user1.id}`).loginAs(user1).json({
      email: user1.email,
      first_name: user1.first_name,
      last_name: 'Doe',
      bio: 'hello world',
    })

    res.assertStatus(200)
    res.assertBodyContains({ last_name: 'Doe', bio: 'hello world' })
  })
})
