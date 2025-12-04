import { Injectable } from '@nestjs/common';
import { CreateBidDto } from './dto/create-bid.dto';
import { UpdateBidDto } from './dto/update-bid.dto';
import { PrismaService } from 'src/prisma.service';
import { PrismaClient } from '@prisma/client';
import { bid } from '@prisma/client';

@Injectable()
export class BidsService {
  constructor(private prisma: PrismaService) {} 
  async create(createBidDto: CreateBidDto) {
    return await this.prisma.bid.create({
      data: {
        title: createBidDto['title'],
        url: createBidDto['url'],
        status: createBidDto['status'],
        location: createBidDto['location'],
        city: createBidDto['city'],
        bid_type: createBidDto['bid_type'],
        deletedAt: null
      }
    })
  }

  // This method takes a Bid ID, and SOFT DELETES it by setting deleted_at to Current Time
  async deleteBid(bidID: number) {
    console.log("Delete bid: ", bidID)
    console.log("type: ", typeof bidID)
    let bid = await this.prisma.bid.findUnique({
      where: {
        id: bidID
      }
    })

    const updateBid = await this.prisma.bid.update({
      where: {
        id: bidID
      },
      data: {
        deletedAt: new Date(),
      },
    })

  }

  async findAll() {
    return await this.prisma.bid.findMany({
      where: {
          deletedAt: null
      }
    });
  }

  async findBidsWithinDistance(homeLat: number, homeLong: number, sliderValue: number) {
    const radiusInMeters = sliderValue * 1609.34; // Convert miles to meters
  
    const locations = await this.prisma.$queryRaw`
      SELECT *, ST_DistanceSphere(
        ST_SetSRID(ST_MakePoint(${homeLong}, ${homeLat}), 4326),
        ST_SetSRID(ST_Point(ST_Y(location::geometry), ST_X(location::geometry)), 4326)
      ) AS distance_in_meters
      FROM public.bid
      WHERE ST_DistanceSphere(
        ST_SetSRID(ST_MakePoint(${homeLong}, ${homeLat}), 4326),
        ST_SetSRID(ST_Point(ST_Y(location::geometry), ST_X(location::geometry)), 4326)
      ) <= ${radiusInMeters};
    `;
    
    return locations;
  }

  async findBidsbyTypeAndDistance(sliderValue: number, bid_type: string) {
    const radiusInMeters = sliderValue * 1609.34; // Convert miles to meters
    let homeLat = 37.3387
    let homeLong = -121.8853
    const locations = await this.prisma.$queryRaw`
      SELECT *, ST_DistanceSphere(
        ST_SetSRID(ST_MakePoint(${homeLong}, ${homeLat}), 4326),
        ST_SetSRID(ST_Point(ST_Y(location::geometry), ST_X(location::geometry)), 4326)
      ) AS distance_in_meters
      FROM public.bid
      WHERE ST_DistanceSphere(
        ST_SetSRID(ST_MakePoint(${homeLong}, ${homeLat}), 4326),
        ST_SetSRID(ST_Point(ST_Y(location::geometry), ST_X(location::geometry)), 4326)
      ) <= ${radiusInMeters}
      AND bid_type = ${bid_type};
    `;
    return locations;

  }

  findOne(id: number) {
    console.log("in find one")
    return `This action returns a #${id} bid`;
  }

  update(id: number, updateBidDto: UpdateBidDto) {
    console.log("in update")
    return `This action updates a #${id} bid`;
  }

  remove(id: number) {
    console.log("in remove")
    return `This action removes a #${id} bid`;
  }
}
