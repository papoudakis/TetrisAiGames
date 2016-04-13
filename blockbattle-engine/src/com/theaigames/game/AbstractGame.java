// Copyright 2015 theaigames.com (developers@theaigames.com)

//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at

//        http://www.apache.org/licenses/LICENSE-2.0

//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.
//	
//    For the full copyright and license information, please view the LICENSE
//    file that was distributed with this source code.

package com.theaigames.game;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.theaigames.engine.Engine;
import com.theaigames.engine.Logic;
import com.theaigames.engine.io.IOPlayer;

/**
 * abstract class AbstractGame
 * 
 * DO NOT EDIT THIS FILE
 * 
 * Extend this class with your main method. In the main method, create an
 * instance of your Logic and run setupEngine() and runEngine()
 * 
 * @author Jim van Eeden <jim@starapple.nl>
 */

public abstract class AbstractGame implements Logic {

	public Engine engine;
	public GameHandler processor;
	
	public int maxRounds;
	
	public boolean DEV_MODE = false; // turn this on for local testing
	public String TEST_BOT; // command for the test bot in DEV_MODE
	public int NUM_TEST_BOTS; // number of bots for this game
	
	public AbstractGame() {
		maxRounds = -1; // set this later if there is a maximum amount of rounds for this game
	}

	/**
	 * Partially sets up the engine
	 * @param args : command line arguments passed on running of application
	 * @throws IOException
	 * @throws RuntimeException
	 */
	public void setupEngine(String args[]) throws IOException, RuntimeException {
		
		// create engine
		this.engine = new Engine();
		
		// add the test bots if in DEV_MODE
		if(DEV_MODE) {
			if(TEST_BOT.isEmpty()) {
				throw new RuntimeException("DEV_MODE: Please provide a command to start the test bot by setting 'TEST_BOT' in your main class.");
			}
			if(NUM_TEST_BOTS <= 0) {
				throw new RuntimeException("DEV_MODE: Please provide the number of bots in this game by setting 'NUM_TEST_BOTS' in your main class.");
			}
			
			for(int i = 0; i < NUM_TEST_BOTS; i++) {
				this.engine.addPlayer(TEST_BOT, "ID_" + i);
			}
			
			return;
		}
		
		// add the bots from the arguments if not in DEV_MODE
		List<String> botDirs = new ArrayList<String>();
		List<String> botIds = new ArrayList<String>();
		
		if (args.length <= 0) {
			throw new RuntimeException("No arguments provided.");
		}
		
		for(int i=0; i < args.length; i++) {
			botIds.add(i + "");
			botDirs.add(args[i]);
		}
		
		// check if the starting arguments are passed correctly
		if(botIds.isEmpty() || botDirs.isEmpty() || botIds.size() != botDirs.size())
			throw new RuntimeException("Missing some arguments.");
		
		// add the players
		for(int i=0; i < botIds.size(); i++) {
			this.engine.addPlayer(botDirs.get(i), botIds.get(i));
		}
	}
	
	/**
	 * Implement this class. Set logic in the engine and start it to run the game
	 */
	protected abstract void runEngine() throws Exception;
	
	/**
	 * @return : True when the game is over
	 */
	@Override
	public boolean isGameOver()
	{
		if (this.processor.isGameOver() 
				|| (this.maxRounds >= 0 && this.processor.getRoundNumber() > this.maxRounds) ) {
        	return true;
        }
        return false;
	}
	
	/**
	 * Play one round of the game
	 * @param roundNumber : round number
	 */
	@Override
    public void playRound(int roundNumber) 
	{
		for(IOPlayer ioPlayer : this.engine.getPlayers())
			ioPlayer.addToDump(String.format("Round %d", roundNumber));
		
		this.processor.playRound(roundNumber);
	}
	
	/**
	 * close the bot processes, save, exit program
	 */
	@Override
	public void finish() throws Exception
	{
		// stop the bots
		for(IOPlayer ioPlayer : this.engine.getPlayers())
			ioPlayer.finish();
		Thread.sleep(100);
		
		if(DEV_MODE) { // print the game file when in DEV_MODE
			String playedGame = this.processor.getPlayedGame();
			System.out.println(playedGame);
		} else { // save the game to database
			try {
				this.saveGame();
			} catch(Exception e) {
				e.printStackTrace();
			}
		}
		
		System.out.println("Done.");
		
        System.exit(0);
	}
	
	/**
	 * Does everything that is needed to store the output of a game
	 */
	public void saveGame() {
		
		// save results to file here
		String playedGame = this.processor.getPlayedGame();
		//~ System.out.println(playedGame);
        if (this.processor.getWinner()!= null){
            System.err.println(this.processor.getWinner().getName());
        }
        else{
           System.err.println("draw");
       }
        
        System.err.flush();
	}
}
