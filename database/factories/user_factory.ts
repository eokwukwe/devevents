import factory from '@adonisjs/lucid/factories'
import User from '#models/user/index'
import hash from '@adonisjs/core/services/hash'

export const UserFactory = factory
  .define(User, async ({ faker }) => {
    return {
      first_name: faker.person.firstName(),
      last_name: faker.person.lastName(),
      email: faker.internet.email(),
      password: await hash.make('password'), // password
    }
  })
  .build()
