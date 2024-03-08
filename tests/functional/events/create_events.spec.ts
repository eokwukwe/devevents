import { DateTime } from 'luxon'
import { test } from '@japa/runner'

import User from '#models/user/index'
import Category from '#models/event/category'
import { UserFactory } from '#database/factories/user_factory'
import { CategoryFactory } from '#database/factories/category_factory'

test.group('Create Events Resource', (group) => {
  let user: User
  let categories: Category[]

  group.setup(async () => {
    user = await UserFactory.create()
    categories = await CategoryFactory.createMany(5)
  })
  test('validate required fields', async ({ client }) => {
    const res = await client.post('/events').loginAs(user).json({})

    res.assertStatus(422)
    res.assertBody({
      errors: {
        title: 'The title field is required',
        description: 'The description field is required',
        attendee_total: 'The attendee_total field is required',
        venue: 'The venue field is required',
        date: 'The date field is required',
        category_id: 'The category_id field is required',
      },
    })
  })

  test('validate field types', async ({ client }) => {
    const res = await client.post('/events').loginAs(user).json({
      title: 1234,
      description: 123453,
      attendee_total: '1234',
      venue: 12345,
      date: 234333,
      category_id: '1234',
    })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        title: 'The value of title field must be a string',
        description: 'The value of description field must be a string',
        attendee_total: 'The attendee_total field must be a number',
        venue: 'The value of venue field must be a string',
        date: 'The date field must be a datetime value',
        category_id: 'The category_id field must be a number',
      },
    })
  })

  test('validate date is greater than or equal to today', async ({ client }) => {
    const res = await client.post('/events').loginAs(user).json({
      title: 'title',
      description: 'description',
      attendee_total: 10,
      venue: '13 bankole street, oregun, lagos',
      date: '2021-01-01',
      category_id: categories[0].id,
    })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        date: 'The date field must be a date after or equal to today',
      },
    })
  })

  test('validate that category exists', async ({ client }) => {
    const res = await client
      .post('/events')
      .loginAs(user)
      .json({
        title: 'title',
        description: 'description',
        attendee_total: 10,
        venue: '13 bankole street, oregun, lagos',
        date: DateTime.now().toISODate(),
        category_id: categories.length + 1,
      })

    res.assertStatus(422)
    res.assertBody({
      errors: {
        category_id: 'The selected category_id is invalid',
      },
    })
  })

  test('create event', async ({ client }) => {
    const res = await client.post('/events').loginAs(user).json({
      title: 'title',
      description: 'description',
      attendee_total: 10,
      venue: '13 bankole street, oregun, lagos',
      date: DateTime.now().toISODate(),
      category_id: categories[0].id,
    })

    res.assertStatus(201)
    res.assertBodyContains({
      title: 'title',
      description: 'description',
      attendee_total: 10,
      venue: '13 bankole street, oregun, lagos',
      category_id: categories[0].id,
    })
  })
})
