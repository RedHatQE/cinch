import jenkins.model.*;
import java.util.logging.Logger;
import org.jvnet.hudson.plugins.thinbackup.*;

Logger logger = Logger.getLogger("jenkins.groovy.Maintenance");
def jenkins = Jenkins.getActiveInstance();
def thinbackup = ThinBackupPluginImpl.getInstance();
boolean changes = false;

String backupPath = "{{ jenkins_backup.directory|default('/jenkins_backup/.backups') }}";
String fullBackupSchedule = "{{ jenkins_backup.full_schedule|default('H 0 * * 0') }}";
String diffBackupSchedule = "{{ jenkins_backup.diff_schedule|default('H 0 * * *') }}";
String excludedFiles = "{{ jenkins_backup.exclude|default('') }}";
def maxSets = {{ jenkins_backup.max_sets|default(4) }};
def waitForIdle = {{ jenkins_backup.wait_for_idle|default(false)|to_json }};
def forceQuietModeTimeout = {{ jenkins_backup.quiet_mode_timeout|default(120)|to_json }};
def backupBuildResults = {{ jenkins_backup.build_results|default(false)|to_json }};
def backupUserContents = {{ jenkins_backup.user_contents|default(false)|to_json }};
def cleanupDiff = {{ jenkins_backup.cleanup_diffs|default(false)|to_json }};
def backupNextBuildNumber = {{ jenkins_backup.next_build_number|default(false)|to_json }};
def moveOldBackupsToZipFile = {{ jenkins_backup.move_to_zip|default(false)|to_json }};
def backupPluginArchives = {{ jenkins_backup.plugin_archives|default(false)|to_json }};

def void changed(String field, def value) {
	changes = true;
	println "CHANGED: Updated " + field + " to " + value;
}

if( !thinbackup.getBackupPath().equals(backupPath) ){
	thinbackup.setBackupPath(backupPath);
	changed("backup path", backupPath);
}
if( !thinbackup.getFullBackupSchedule().equals(fullBackupSchedule) ) {
	thinbackup.setFullBackupSchedule(fullBackupSchedule);
	changed("full backup schedule", fullBackupSchedule);
}
if( !thinbackup.getDiffBackupSchedule().equals(diffBackupSchedule) ){
	thinbackup.setDiffBackupSchedule(diffBackupSchedule);
	changed("diff backup schedule", diffBackupSchedule);
}
if( thinbackup.getNrMaxStoredFull() != maxSets ) {
	thinbackup.setNrMaxStoredFull(maxSets);
	changed("max number of backups stored", maxSets);
}
if( !thinbackup.getExcludedFilesRegex().equals(excludedFiles) ) {
	thinbackup.setExcludedFilesRegex(excludedFiles);
	changed("excluded files", excludedFiles);
}
if( thinbackup.isWaitForIdle() != waitForIdle ) {
	thinbackup.setWaitForIdle(waitForIdle);
	changed("wait for idle", waitForIdle);
}
if( thinbackup.getForceQuietModeTimeout() != forceQuietModeTimeout ) {
	thinbackup.setForceQuietModeTimeout(forceQuietModeTimeout);
	changed("force quiet mode timeout", forceQuietModeTimeout);
}
if( thinbackup.isBackupBuildResults() != backupBuildResults ) {
	thinbackup.setBackupBuildResults(backupBuildResults);
	changed("backup build results", backupBuildResults);
}
if( thinbackup.isBackupUserContents() != backupUserContents ) {
	thinbackup.setBackupUserContents(backupUserContents);
	changed("backup user contents", backupUserContents);
}
if( thinbackup.isCleanupDiff() != cleanupDiff ) {
	thinbackup.setCleanupDiff(cleanupDiff);
	changed("cleanup diffs", cleanupDiff);
}
if( thinbackup.isBackupNextBuildNumber() != backupNextBuildNumber ) {
	thinbackup.setBackupNextBuildNumber(backupNextBuildNumber);
	changed("backup next build number", backupNextBuildNumber);
}
if( thinbackup.isMoveOldBackupsToZipFile() != moveOldBackupsToZipFile ) {
	thinbackup.setMoveOldBackupsToZipFile(moveOldBackupsToZipFile);
	changed("move old backups to zip", moveOldBackupsToZipFile);
}

if( thinbackup.isBackupPluginArchives() != backupPluginArchives ) {
	thinbackup.setBackupPluginArchives(backupPluginArchives);
	changed("backup plugin archives", backupPluginArchives);
}

if( changes && !checkMode )
	thinbackup.save();
