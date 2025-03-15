package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.util.formatFileSize
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.FileDashboardViewModel
import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileInfo
import java.text.SimpleDateFormat
import java.util.Locale


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FileDashboardScreen(
    modifier: Modifier = Modifier,
    viewModel: FileDashboardViewModel = viewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Files Dashboard") },
                actions = {
                    IconButton(onClick = { viewModel.fetchFiles() }) {
                        Icon(
                            imageVector = Icons.Default.Refresh,
                            contentDescription = "Refresh"
                        )
                    }
                }
            )
        }
    ) { paddingValues ->
        Box(
            modifier = modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            when {
                uiState.isLoading -> LoadingIndicator()
                uiState.error != null -> ErrorView(error = uiState.error!!, onRetry = { viewModel.fetchFiles() })
                uiState.files.isEmpty() -> EmptyFilesView()
                else -> FilesList(files = uiState.files)
            }
        }
    }
}

@Composable
private fun LoadingIndicator() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}

@Composable
private fun ErrorView(error: String, onRetry: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Error: $error",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.error
        )
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = onRetry) {
            Text("Retry")
        }
    }
}

@Composable
private fun EmptyFilesView() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Icon(
            imageVector = Icons.Default.Delete,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.5f)
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "No files available",
            style = MaterialTheme.typography.titleMedium
        )
    }
}

@Composable
private fun FilesList(files: List<FileInfo>) {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(items = files) { file ->
            FileItem(file = file)
        }
    }
}

@Composable
private fun FileItem(file: FileInfo) {
    val formattedDate = remember(file.updatedAt) {
        val formatter = SimpleDateFormat("MMM dd, yyyy - HH:mm", Locale.getDefault())
        formatter.format(file.updatedAt)
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { /* Handle click */ },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // File type icon
            Icon(
                imageVector = when {
                    file.contentType.startsWith("image/") -> Icons.Filled.ShoppingCart // TODO change this
                    file.contentType.startsWith("video/") -> Icons.Default.ShoppingCart
                    file.contentType.startsWith("audio/") -> Icons.Default.ShoppingCart
                    file.contentType.startsWith("text/") -> Icons.Default.ShoppingCart
                    file.contentType.startsWith("application/pdf") -> Icons.Default.ShoppingCart
                    else -> Icons.Default.ShoppingCart
                },
                contentDescription = null,
                modifier = Modifier.size(40.dp),
                tint = MaterialTheme.colorScheme.primary
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = file.fileName,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )

                Spacer(modifier = Modifier.height(4.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = file.size.formatFileSize(),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.outline
                    )

                    Text(
                        text = formattedDate,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.outline
                    )
                }
            }
        }
    }
}


//@Composable
//fun DashboardScreen(
//    userData: UserData?,
//
//){
//    Column {
//        Box(
//            modifier = Modifier
//                .fillMaxWidth()
//                .fillMaxHeight(.11f)
//                .background(Color("#3182ce".toColorInt()))
//        ) {
//            Row(
//                modifier = Modifier
//                    .padding(top = 50.dp, start = 10.dp)
//                    .fillMaxWidth()
//            ) {
//                Text(
//                    text = "Pitless Bucket",
//                    fontFamily = fontFamily,
//                    fontWeight = FontWeight.ExtraBold,
//                    color = Color.White,
//                    fontSize = 25.sp
//                )
//            }
//        }
//        Box(
//            modifier = Modifier
//                .fillMaxWidth()
//                .fillMaxHeight(.04f)
//                .background(Color.White),
//            contentAlignment = Alignment.Center
//        ) {
//            Text(
//                text = "Your Files & Folders",
//                fontWeight = FontWeight.Bold,
//                color = Color.Black,
//                fontSize = 20.sp,
//                textAlign = TextAlign.Center
//            )
//        }
//    }
//}