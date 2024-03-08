import { DateTime } from 'luxon'
import { test } from '@japa/runner'

import User from '#models/user/index'
import Event from '#models/event/event'
import { UserFactory } from '#database/factories/user_factory'
import { EventFactory } from '#database/factories/event_factory'

test.group('Update|Delete Events Resource', (group) => {
  let user: User
  let events: Event[]

  group.setup(async () => {
    user = await UserFactory.create()
    events = await EventFactory.merge({ userId: user.id }).createMany(10)
  })
  test('Update - user can only update their event', async ({ client }) => {
    const user2 = await UserFactory.create()
    const res = await client.put(`/events/${events[0].id}`).loginAs(user2).json({
      title: 'title',
      description: 'description',
      attendee_total: 10,
      venue: '13 bankole street, oregun, lagos',
      date: DateTime.now().toISODate(),
      category_id: events[0].categoryId,
    })

    res.assertStatus(403)
    res.assertBody({ message: 'Unauthorized access' })
  })

  test('Update - user can update event', async ({ client }) => {
    const titleUpdate = 'title updated'

    const res = await client.put(`/events/${events[0].id}`).loginAs(user).json({
      title: titleUpdate,
      description: 'description',
      attendee_total: 10,
      venue: '13 bankole street, oregun, lagos',
      date: DateTime.now().toISODate(),
      category_id: events[0].categoryId,
    })

    res.assertStatus(200)
    res.assertBodyContains({ title: titleUpdate })
  })

  test('Delete - user can only delete their event', async ({ client }) => {
    const user2 = await UserFactory.create()
    const res = await client.delete(`/events/${events[0].id}`).loginAs(user2)

    res.assertStatus(403)
    res.assertBody({ message: 'Unauthorized access' })
  })

  test('Delete - user can delete their event', async ({ client }) => {
    const res = await client.delete(`/events/${events[0].id}`).loginAs(user)

    res.assertStatus(204)
  })
})
