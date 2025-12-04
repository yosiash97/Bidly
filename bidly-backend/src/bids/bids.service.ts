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
    const radiusInMiles = sliderValue;

    // Get all bids and filter by distance using Haversine formula
    const allBids = await this.prisma.bid.findMany({
      where: {
        deletedAt: null,
        location: {
          not: null
        }
      }
    });

    // Helper function to calculate distance using Haversine formula
    const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
      const R = 3959; // Earth's radius in miles
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c;
    };

    // Filter bids within the specified radius
    const filteredBids = allBids.filter(bid => {
      if (!bid.location) return false;

      // Parse location string (format: "POINT(lat long)")
      const match = bid.location.match(/POINT\s*\(?\s*([-\d.]+)\s+([-\d.]+)\s*\)?/i);
      if (!match) return false;

      const bidLat = parseFloat(match[1]);
      const bidLong = parseFloat(match[2]);

      const distance = calculateDistance(homeLat, homeLong, bidLat, bidLong);
      return distance <= radiusInMiles;
    }).map(bid => ({
      ...bid,
      distance_in_miles: bid.location ? (() => {
        const match = bid.location.match(/POINT\s*\(?\s*([-\d.]+)\s+([-\d.]+)\s*\)?/i);
        if (!match) return null;
        const bidLat = parseFloat(match[1]);
        const bidLong = parseFloat(match[2]);
        return calculateDistance(homeLat, homeLong, bidLat, bidLong);
      })() : null
    }));

    return filteredBids;
  }

  async findBidsbyTypeAndDistance(sliderValue: number, bid_type: string) {
    const radiusInMiles = sliderValue;
    let homeLat = 37.3387
    let homeLong = -121.8853

    // Get all bids of the specified type and filter by distance using Haversine formula
    const allBids = await this.prisma.bid.findMany({
      where: {
        deletedAt: null,
        bid_type: bid_type,
        location: {
          not: null
        }
      }
    });

    // Helper function to calculate distance using Haversine formula
    const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
      const R = 3959; // Earth's radius in miles
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c;
    };

    // Filter bids within the specified radius
    const filteredBids = allBids.filter(bid => {
      if (!bid.location) return false;

      // Parse location string (format: "POINT(lat long)")
      const match = bid.location.match(/POINT\s*\(?\s*([-\d.]+)\s+([-\d.]+)\s*\)?/i);
      if (!match) return false;

      const bidLat = parseFloat(match[1]);
      const bidLong = parseFloat(match[2]);

      const distance = calculateDistance(homeLat, homeLong, bidLat, bidLong);
      return distance <= radiusInMiles;
    }).map(bid => ({
      ...bid,
      distance_in_miles: bid.location ? (() => {
        const match = bid.location.match(/POINT\s*\(?\s*([-\d.]+)\s+([-\d.]+)\s*\)?/i);
        if (!match) return null;
        const bidLat = parseFloat(match[1]);
        const bidLong = parseFloat(match[2]);
        return calculateDistance(homeLat, homeLong, bidLat, bidLong);
      })() : null
    }));

    return filteredBids;
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
