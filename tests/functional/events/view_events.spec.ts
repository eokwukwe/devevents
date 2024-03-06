import { test } from '@japa/runner'

import Category from '#models/event/category'
import { CategoryFactory } from '#database/factories/category_factory'

test.group('Events view Resource', (group) => {
  let categories: Category[]

  group.setup(async () => {
    categories = await CategoryFactory.createMany(6)
  })
  test('get event categories', async ({ assert, client }) => {
    const res = await client.get('/events/categories')

    res.assertStatus(200)
    assert.equal(categories.length, res.body().length)
  })
})
