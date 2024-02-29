import { test } from '@japa/runner'

import { UserFactory } from '#database/factories/user_factory'
import User from '#models/user/index'

test.group('View User Resource', (group) => {
  let user: User
  let users: User[]

  group.setup(async () => {
    user = await UserFactory.create()
    users = await UserFactory.createMany(5)
  })

  test('get single user', async ({ client }) => {
    const res = await client.get(`/users/${users[0].id}`).loginAs(user)

    res.assertStatus(200)
    res.assertBodyContains({ first_name: users[0].first_name })
  })

  test('get all users', async ({ client, assert }) => {
    const res = await client.get(`/users`).loginAs(user)

    res.assertStatus(200)

    const allUsers = await User.all()
    assert.equal(allUsers.length, res.body().meta.total)
  })
})
