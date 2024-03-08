import app from '@adonisjs/core/services/app'
import { Client, LatLngLiteral } from '@googlemaps/google-maps-services-js'

import { googleAPIKey } from '#config/app'

class GooglMapServices {
  #client: Client

  constructor() {
    this.#client = new Client({})
  }

  async getLatLng(address: string): Promise<LatLngLiteral> {
    // if test environment fake the request
    if (app.inTest) {
      return { lat: 45, lng: -110 }
    }

    try {
      const response = await this.#client.geocode({
        params: {
          address,
          key: googleAPIKey,
        },
      })

      return response.data.results[0].geometry.location
    } catch (error) {
      throw error
    }
  }
}

export default new GooglMapServices()
