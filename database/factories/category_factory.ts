import factory from '@adonisjs/lucid/factories'
import Category from '#models/event/category'

export const CategoryFactory = factory
  .define(Category, async ({ faker }) => {
    return {
      name: faker.lorem.word({ length: { min: 3, max: 9 } }),
    }
  })
  .build()
