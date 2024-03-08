import factory from '@adonisjs/lucid/factories'
import { DateTime } from 'luxon'

import Event from '#models/event/event'
import { CategoryFactory } from './category_factory.js'
import { UserFactory } from './user_factory.js'
import Category from '#models/event/category'
import User from '#models/user/index'

export const EventFactory = factory
  .define(Event, async ({ faker }) => {
    let users = await User.all()
    let categories = await Category.all()

    // This is added to prevent duplicate entries in the database
    // when running tests
    if (!categories.length) {
      categories = await CategoryFactory.createMany(5)
    }

    if (!users.length) {
      users = await UserFactory.createMany(5)
    }

    return {
      title: faker.lorem.words(3),
      description: faker.lorem.paragraph(),
      attendee_total: faker.number.int({ min: 1, max: 100 }),
      venue: faker.location.streetAddress(),
      venueLat: faker.location.latitude(),
      venueLng: faker.location.longitude(),
      date: DateTime.fromJSDate(faker.date.future()),
      category_id: faker.number.int({ min: 1, max: categories.length }),
      user_id: faker.number.int({ min: 1, max: users.length }),
    }
  })
  .build()
