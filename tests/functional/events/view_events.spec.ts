import { test } from '@japa/runner'

import User from '#models/user/index'
import Event from '#models/event/event'
import Category from '#models/event/category'
import { UserFactory } from '#database/factories/user_factory'
import { EventFactory } from '#database/factories/event_factory'
import { CategoryFactory } from '#database/factories/category_factory'

test.group('View Events Resource', (group) => {
  let user: User
  let events: Event[]
  let categories: Category[]

  group.setup(async () => {
    user = await UserFactory.create()
    categories = await CategoryFactory.createMany(6)

    events = await EventFactory.merge({
      categoryId: categories[0].id,
    }).createMany(10)
  })
  test('get event categories', async ({ client }) => {
    const res = await client.get('/events/categories')

    res.assertStatus(200)
  })

  test('get all events', async ({ assert, client }) => {
    const res = await client.get('/events')

    res.assertStatus(200)
    assert.equal(events.length, res.body().data.length)
  })

  test('get single event', async ({ assert, client }) => {
    const event = events[0]

    const res = await client.get(`/events/${event.id}`)

    res.assertStatus(200)
    assert.equal(event.title, res.body().title)
  })

  test('return 404 when event does not exist', async ({ client }) => {
    const res = await client.get(`/events/${events.length * 10}`)

    res.assertStatus(404)
    res.assertBody({
      message: 'Resource not found',
    })
  })
})
