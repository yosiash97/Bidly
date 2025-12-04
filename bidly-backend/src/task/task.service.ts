import { Injectable } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';
import { exec } from 'child_process';
import * as fs from 'fs';
import { HttpService } from '@nestjs/axios';
import { BidsService } from 'src/bids/bids.service';
import { PrismaService } from 'src/prisma.service';
import { PrismaClient, Prisma } from '@prisma/client';
import { bid } from '@prisma/client';

@Injectable()
export class TaskService {
  constructor(
    private readonly httpService: HttpService,
    private readonly bidsService: BidsService,
    private prisma: PrismaService
    ) {}
  private readonly jsonFilePath = process.env.NODE_ENV === 'production'
  ? "cities.json"
  : "/Users/yosiashailu/Desktop/bidly-backend/cities.json";
  private readonly outputData: any[] = [];

  @Cron('0 0 * * 0')
  async executeGptScraper() {
    try {
      const jsonFileContent = fs.readFileSync(this.jsonFilePath, 'utf-8');
      const urls = JSON.parse(jsonFileContent);

      const promises = [];

      for (let [city, url] of Object.entries(urls)) {
        await this.scrapeLatestBidsWithDelay(String(url), city);      }
      
      await this.loadScrapedBidsIntoDB();

      // After all data is collected, you can insert it into the database
      // this.insertIntoDatabase(this.outputData);
    } catch (error) {
      console.error('Error executing GPT scraper:', error);
    }
  }

  private async scrapeLatestBidsWithDelay(url: string, city: string): Promise<void> {
    await this.scrapeLatestBids(url, city);
    await this.delay(30000); // 30 seconds delay
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async loadScrapedBidsIntoDB() {
    console.log("Output data: ", this.outputData)
    if (this.outputData.length == 0) {
      return;
    }
    let arrayOfBids = await this.outputData
    let point;
    for (let bid of arrayOfBids ) {
      console.log("Bid Geo Location: ", bid['geo_location'])
      if (bid['geo_location']) {
        point = `POINT(${bid['geo_location'][0]} ${bid['geo_location'][1]})`;
      }
      else {
        point = `POINT(39.7886111 -82.6418883)`;
      }
      

      try {
        await this.bidsService.create({
          title: bid.title,
          url: bid.url, 
          status: bid.status,
          location: point,
          city: bid.city,
          bid_type: bid.bid_type
        })
      } catch (error) {
        if (error instanceof Prisma.PrismaClientKnownRequestError && error.code === 'P2002') {
          console.error(`A unique constraint violation occurred for the title: ${bid.title}. This bid already exists in the database.`);
        } else {
          console.error('An unexpected error occurred:', error);
        }
      }

    }
  }

  //From FE we have a coordinate X, Y and want to send request for all geocoordinates between 20 miles
  private async scrapeLatestBids(url: string, city: string): Promise<void> {
    try {
      const escapedCity = city.replace(/ /g, '\\ '); 
      const pythonPath = process.env.NODE_ENV === 'production' ? '/app/venv/bin/python3' : '/Users/yosiashailu/Desktop/bidly-backend/myenv/bin/python3';

      console.log(`${pythonPath} scraper.py "${url}" "${escapedCity}"`);
      // Execute the Python script using promisified version of exec
      const { stdout, stderr } = await this.promisifyExec(`${pythonPath} scraper.py "${url}" "${escapedCity}"`);

      try {
        // Extract JSON string from stdout using regex
        const jsonMatches = stdout.match(/\[\s*\{.*?\}\s*\]/gs);
            
        if (jsonMatches) {
          const jsonString = jsonMatches[jsonMatches.length - 1];
          try {
              const dataArray = JSON.parse(jsonString);
              console.log("Data Array: ", dataArray)
              this.outputData.push(...dataArray);  // Push the parsed data into outputData array
              console.log("After push: ", this.outputData)
          } catch (jsonError) {
              console.error("Error parsing JSON string:", jsonError);
              console.log("Raw JSON string: ", jsonString);
          }
          if (stderr) {
            console.log("in stderr if")
            console.error('Python script error:', stderr);
          }
          } else {
              throw new Error("No JSON data found in stdout");
          }
      } catch (jsonError) {
          console.log("Error parsing stdout as JSON:");
          console.error(jsonError);
      }
      if (stderr) {
        console.error('Python script error:', stderr);
      }
    } catch (error) {
      console.error('Error executing Python script for: ', city, error);
    }
  }

  // Promisify the exec function
  private promisifyExec(command: string): Promise<{ stdout: string, stderr: string }> {
    return new Promise((resolve, reject) => {
      exec(command, (error, stdout, stderr) => {
        if (error) {
          reject(error);
        } else {
          resolve({ stdout, stderr });
        }
      });
    });
  }
}
