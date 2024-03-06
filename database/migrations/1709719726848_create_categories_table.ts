import { BaseSchema } from '@adonisjs/lucid/schema'

export default class extends BaseSchema {
  protected tableName = 'categories'

  async up() {
    this.schema.createTable(this.tableName, (table) => {
      table.increments('id').primary()
      table.string('name').notNullable().unique()
    })

    this.defer(async (db) => {
      await db
        .table('categories')
        .multiInsert([
          { name: 'Drinks' },
          { name: 'Culture' },
          { name: 'Film' },
          { name: 'Food' },
          { name: 'Music' },
          { name: 'Travel' },
        ])
    })
  }

  async down() {
    this.schema.dropTable(this.tableName)
  }
}
