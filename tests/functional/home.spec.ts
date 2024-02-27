import { test } from '@japa/runner'

test.group('Home', () => {
  test('example test', async ({ client }) => {
    const res = await client.get('/')

    res.assertStatus(200)
    res.assertBody({ message: 'Welcome to Devevents AdonisJS API!' })
  })
})
